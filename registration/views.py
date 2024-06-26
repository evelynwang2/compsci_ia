from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import School, Country, Race, State, Delegate, Team, Delegation, Registry, Advisor
from django.db import connection, DatabaseError, IntegrityError
from .forms import RegisterIndForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# home page, if user is authenticated, get advisor info  
def home(request):
    user = request.user
    # if user log in, check advisor information to display either "my delegation " or create delegation
    # whenever loading homepage
    if user.is_authenticated:
        try:
            advisor = Advisor.objects.get(user=user)
            return render(request, 'home.html', {'advisor':advisor})
        except Advisor.DoesNotExist:
            return render(request, 'home.html') 
    else:
      return render(request, 'home.html')

# display a delegate's details
def displayDelegate(request, delegate_id):
    delegate = get_object_or_404(Delegate, pk=delegate_id)
    return render(request, 'display_delegate.html'
                         , {'delegate':delegate} )

# display a delegation team information
def displayDelegation(request, delegation_id):
    delegation = get_object_or_404(Delegation, pk=delegation_id)
    delegateIndex = [1,2,3,4]
    return render(request, 'display_delegation.html'
                         , {'delegation':delegation,'delegateIndex':delegateIndex} )

# get all unassigned countries
def getUnassignedCountries():
    # Get IDs of countries already assigned to delegations
    assignedCountryIds = Delegation.objects.values_list('assignedCountry_id', flat=True)
    
    # Query countries that are not in the list of assigned country IDs
    unassignedCountries = Country.objects.exclude(id__in=assignedCountryIds).order_by('name')
    return unassignedCountries

# dummy registration for tessting
def registration(request):
    # return HttpResponse('<h1>Welcome home page</h1>')
    schools = School.objects.all().order_by('name')
    ## countries = Country.objects.all()
    countries = getUnassignedCountries()
    races = Race.objects.all().order_by('race')
    states = State.objects.all().order_by('stateNameLong')

    ## create two index for looping display delegate (4) and countries (10)
    index10 = [1,2,3,4,5,6,7,8,9,10]
    index4 = [1,2,3,4]
    return render(request, 'registration_whole.html',
                  {'schools':schools, 
                   'countries':countries, 
                   'races':races,
                   'states':states,
                   'index10':index10,
                   'index4':index4
                  })

# validate individual delegate input 
def validateIndInput(request):
    errors = []
    inputSchoolId = request.POST.get('school')
    inputRaceId = request.POST.get('race')
    inputStateId = request.POST.get('state')
    

    # 'Choose... is defaul choice of option input fields
    #    such as school, race, state, role, gender, race
    # (123) 456-7890 is place holder of delegate mobile phone
    # (987) 65403210 is place holder of delegate parent's phone
    # if any of check failed, append the item to error list 
    if not inputSchoolId or inputSchoolId == 'Choose...':
        errors.append("School")
    if not inputRaceId or inputRaceId == 'Choose...':
        errors.append("Race")
    if not inputStateId or inputStateId == 'Choose...':
        errors.append("State")
    if not request.POST['role'] or inputStateId == 'Choose...':
        errors.append("role")
    if not request.POST['fname']:
        errors.append("First Name")
    if not request.POST['lname']:
        errors.append("Last Name")
    if not request.POST['gender'] or request.POST['gender'] == 'Choose...':
        errors.append("Gender")
    if not request.POST['grade'] or request.POST['grade'] == 'Choose...':
        errors.append("Grade")
    if not request.POST['email']:
        errors.append("Email")
    if not request.POST['phone'] or request.POST['phone'] == '(123) 456-7890':
        errors.append("Phone")
    if not request.POST['addr']:
        errors.append("Street Address")
    if not request.POST['city']:
        errors.append("City")
    if not request.POST['zip']:
        errors.append("Zip")
    if not request.POST['parentName']:
        errors.append("Parent Names")
    if not request.POST['parentEmail']:
        errors.append("Parent Email")
    if not request.POST['parentPhone'] or request.POST['parentPhone'] == '(789) 654-3210':
        errors.append("Parent Phone")

    return errors, inputSchoolId, inputRaceId, inputStateId

# this function is to create an individual delegate 
# corresponding template is: registeration_ind.html
# for GET: return registaration_ind.html
# for POST: 
#   if any errors, return to registration_ind.html
#   if successful creation, redirect to display_delegate.html
# steps needed to create a delegate
#   1. validate input
#   2. create a delegate
def registrationInd(request): 

    ## extract the sorted lists of school, race and state needed for individual delegate registration page
    schools = School.objects.all().order_by('name')
    races = Race.objects.all().order_by('race')
    states = State.objects.all().order_by('stateNameLong')

    # if GET, render registration_ind.html
    if request.method == 'GET':
        return render(request, 'registration_ind.html',
                               {'schools':schools, 
                                'races':races,
                                'states':states,
                               })
    
    # if POST, create invidual delegate
    elif request.method == 'POST':
        # get input validated, if any error, render registration_ind.html with all errors
        errors, inputSchoolId, inputRaceId, inputStateId = validateIndInput(request)
        if errors:
            ## if the list of error is not empty, go back to black registration_ind.html
            return render(request,'registration_ind.html',
                                   {'schools':schools, 
                                    'races':races,
                                    'states':states,
                                    'error': errors
                                   }) 
        
        # all input check passed, now create a new delegete in DB using ORM
        # for forigne key columns, get instances, not just ID, attributes incluing school, race and state
        inputSchool = School.objects.get(id=inputSchoolId)
        inputRace = Race.objects.get(id=inputRaceId)
        inputState = State.objects.get(id=inputStateId)

        # use try ... except to catch exceptions
        # use objects create function to insert a record in Delegate table
        # all fields but year at MUN
        try:
            newDelegate = Delegate.objects.create(role=request.POST['role'],
                                                  firstName=request.POST['fname'],
                                                  lastName=request.POST['lname'],
                                                  gender=request.POST['gender'],
                                                  grade=request.POST['grade'],
                                                  email=request.POST['email'],
                                                  mobilePhone=request.POST['phone'],
                                                  streetAddr=request.POST['addr'],
                                                  city=request.POST['city'],
                                                  zip=request.POST['zip'],
                                                  parentName=request.POST['parentName'],
                                                  parentEmail=request.POST['parentEmail'],
                                                  parentPhone=request.POST['parentPhone'],
                                                  race=inputRace,
                                                  state=inputState,
                                                  school=inputSchool
                                                  )
            
        except DatabaseError as e:
            print(str(e))  # Log the error for debugging purposes
            # in case insertion failed, catch general DatabaseError
            # return the registration_ind.html with the exception message
            return render(request, 'registration_ind.html', 
                                   {'schools':schools, 
                                    'races':races,
                                    'states':states,
                                    'error': 'An error occurred while creating delegate' + str(e)
                                   }) 
        else:
            # Handle successful insertion, display the information of newly create delegate
            return redirect('displayDelegate', newDelegate.id)    

# this is a function to create a team     
# corresponding teamplate: registartion_team.html
# for GET: render registration_team.html
# for POST:
#   if any errors: return to registration_team.html
#   if success: redirect to display_delegation.html
# steps needed to create a team
#   1. validate input
#   2. create up to 4 delegates 
#   3. create a team
#   4. create up to 10 registration, one for each country
#   5. create the deleation  
def registrationTeam(request):

    # extract the sorted lists of schools, unassigned countries, races and states
    # for registration_team.html
    schools = School.objects.all().order_by('name')
    countries = getUnassignedCountries()
    races = Race.objects.all().order_by('race')
    states = State.objects.all().order_by('stateNameLong')
    unassignedCountryIds = countries.values_list('id', flat=True)

    # if GET: render registratoin_team.html
    if request.method == 'GET':
        return render(request, 'registration_team.html', {
            'schools': schools, 
            'countries': countries, 
            'races': races,
            'states': states,
        })

    # if POST: validate input, create delegates, team, registration, and delegation
    # if any errors, return to registration_team.html with error messages
    # if success, display the delegation team just created with assigned country
    elif request.method == 'POST':
        # check: the count of delegate >= 1
        delegateCount = int(request.POST.get('delegateCount', 0))

        if delegateCount == 0:
            # If no delegate information is provided, show error message
            return render(request, 'registration_team.html', {
                'schools': schools, 
                'countries': countries,
                'races': races,
                'states': states,
                'error': 'At least one delegate is required for registration.'
            })

        # check: the count of selected countries >= 1
        countryCount = int(request.POST.get('countryCount', 0))
        if countryCount == 0:
            # If no country information is provided, show error message
            return render(request, 'registration_team.html', {
                'schools': schools, 
                'countries': countries,
                'races': races,
                'states': states,
                'error': 'At least one country is required for registration.'
            })

        # validate and extract POST variable
        # prepare a list to hold all errors
        errors = []

        # check: school is valid, "Choose..." option has no values
        inputSchoolId = request.POST.get('school')
        if not inputSchoolId:
            errors.append('School')
        inputSchool = School.objects.get(id=inputSchoolId)

        # check and extract delegates inputs
        # for each delegate, following fields are required
        # 'fname', 'lname', 'gender', 'race', 'grade',
        # 'munYear', 'email', 'phone', 'addr', 'city',
        # 'state', 'zip', 'parentName', 'parentEmail', 'parentPhone'
        # inputDelegateAttrs is a list of Delegate,
        # each delegate is a dictionary with keys of fields requires, and values from POST
        # loop up to the count of delegats
        # for each delegate, need to prepare append the index to the field name as the KEY
        # for any errors append the field to errors
        # after extract all attributes on a delegate, push the new delegaet dictionary into the delegate list
        inputDelegateAttrs = []
        for i in range(int(delegateCount)):
           delegateAttrs = {}
           for field in ['fname', 'lname', 'gender', 'race', 'grade',
                         'munYear', 'email', 'phone', 'addr', 'city',
                         'state', 'zip', 'parentName', 'parentEmail', 'parentPhone']:

               fieldKey = field + str(i+1)
               fieldValue = request.POST.get(fieldKey)
               delegateAttrs[field] = fieldValue
               if not fieldValue:
                   errors.append(f"Person {i+1}:{field}")
               if field in ['gender', 'race', 'grade', 'munYear', 'state']: 
                   if fieldValue == 'Choose...':
                       errors.append(f"Person {i+1}:{field}")
               if field == 'phone' and fieldValue == '(123) 456-7890':
                   errors.append(f"Person {i+1}:{field}")
               if field == 'parentPhone' and fieldValue == '(987) 654-3210':
                   errors.append(f"Person {i+1}:{field}")

           inputDelegateAttrs.append(delegateAttrs)

        # check and extract countries selected 
        # store all countries id in a list
        # countryIds is a list of country IDs
        # which extracting all countries, check it agaigst unassigned country,
        # if the country is not assigned, then assign the country to the team
        # once assigned country is set, no need to check it any more
        # Note: the POST country choices are ordered
        countryIds = []
        assignedCountryId = None
        for j in range(1, int(countryCount) + 1):
            countryKey = f'inputCountry{j}'
            countryId = request.POST.get(countryKey)
            if not countryId:
               errors.append(f"Country {j}")
            countryIds.append(countryId)

            # assign country if not assigned and it is available 
            if assignedCountryId is None and int(countryId) in unassignedCountryIds:
                assignedCountryId = countryId
             
        # in case any errors with input values, render registration_team.html with all errors
        if errors:  
            print('there are errors')
            # return HttpResponse('An error occurred')
            return render(request, 'registration_team.html', {
                 'schools': schools, 
                 'countries': countries,
                 'races': races,
                 'states': states,
                 'error': errors
            })
    
        # Process the registration
        try:
            # loop throug the inputDelegateAttrs to create delegates, up to 4
            # and save the newly created delegate instance into delegates list 
            # which is needed to create the team
            delegates = []
            for attrs in inputDelegateAttrs:
                inputRace = Race.objects.get(id=attrs['race'])
                inputState = State.objects.get(id=attrs['state'])
                
                newDelegate = Delegate.objects.create(
                    firstName=attrs['fname'],
                    lastName=attrs['lname'],
                    gender=attrs['gender'],
                    grade=attrs['grade'],
                    yearAtMun=attrs['munYear'],
                    email=attrs['email'],
                    mobilePhone=attrs['phone'],
                    streetAddr=attrs['addr'],
                    city=attrs['city'],
                    zip=attrs['zip'],
                    parentName=attrs['parentName'],
                    parentEmail=attrs['parentEmail'],
                    parentPhone=attrs['parentPhone'],
                    race=inputRace,
                    state=inputState,
                    school=inputSchool
                )
                delegates.append(newDelegate)

            # create team 
            # the team has school, delegate1, delegate2, gelegate3, deleage4
            # since it is unknown how any delegates entered, enumerate the delegate attribuite list
            teamData = {'school': inputSchool}
            for i, delegate in enumerate(delegates, start=1):
                teamData[f'delegate{i}'] = delegate

            newTeam = Team.objects.create(**teamData)

            # create registries
            # simlar to delegate of the team, enumerate to create rows for each selected country
            # countries are in row
            for rank, country_id in enumerate(countryIds, start=1):
                newCountry = Country.objects.get(id=country_id)
                Registry.objects.create(team=newTeam, country=newCountry, choiceRank=rank)
            
            # create delegation
            # in case none of the selected country is avaible, set to default value "Unassigned - check email
            if assignedCountryId is None:
                assignedCountry = Country.objects.get(name='Unassigned - check email')
            else:
                assignedCountry = Country.objects.get(id=assignedCountryId)
            newDelegation = Delegation.objects.create(school=inputSchool, team=newTeam, assignedCountry=assignedCountry)
            
        except DatabaseError as e:
            print(str(e))  # Log the error for debugging purposes
            # return HttpResponse('An error occurred while creating delegate: ' + str(e))
            errors.append(str(e))
            
            return render(request, 'registration_team.html', 
                          {'schools': schools, 
                           'races': races,
                           'states': states,
                           'countries': countries,
                           'error': errors
                          }) 
        # redirect to display deleation wit the new delegation objects
        return redirect('displayDelegation', newDelegation.id)


# create a new advisor, basicially to associate the advisor with the school
# because all delegates and delegation are also assoicated with the school
# this fucntion is only for loged in users
# corresponding template: create_advisor_delegation.html
# for GET: retuen create_advisor_delegation.html
# for POST: create a new record in Advisor
# steps needed to creata the connect of advisor and the school
#  1. validate input
#. 2. create a advisor
@login_required
def createAdvisor(request):
    # get the school
    schools = School.objects.all().order_by('name')

    if request.method == 'GET':
        return render(request, 'create_advisor_delegation.html', {'schools':schools})

    elif request.method == 'POST':
        # in case failed, return to create_adviosr_delegation.html
        inputSchoolId = request.POST.get('school')
        if not inputSchoolId or inputSchoolId == 'Choose...':
            return render(request, 'create_advisor_delegation.html', {'schools':schools, 'error': 'Please pick valid school!'})

        inputSchool = School.objects.get(id=inputSchoolId)
        try:
            newAdvisor = Advisor.objects.create(name=request.POST['name'],
                                                school=inputSchool,
                                                user=request.user,
                                                isActive=True
                                               )
            
        except DatabaseError as e:
            print(str(e))  # Log the error for debugging purposes
            return render(request, 'create_advisor_delegation.html', 
                                   {'schools':schools, 
                                    'error': 'Failed to create you delegation' + str(e)
                                   }) 
        else:
            # Handle successful insertion to display the advisor's schools delegation
            return redirect('displayMyDelegation', newAdvisor.id)   
        
# display delegation information for the advisor's school 
# including teams and individuals
# corresponding template: display_advisor_delegation.html
# steps needed
#  1. get Advisor by advisor_id
#. 2. get all teams of advisor's school and team counts
#  3. get all indivudual delegations of advisor's school and individual counts
#  4. render display_advisor_delgation.html with 
#.    advisor instance, a list of teams, the count of teams, a list of individuals, the count of individuals
@login_required
def displayAdvisor(request, advisor_id):
    # get advisor instance by advisor passed in
    advisor = get_object_or_404(Advisor,id=advisor_id)

    # pull all teams associate with adivisor's school 
    advisorTeams = Delegation.objects.filter(school=advisor.school)
    advisorTeamsCount = advisorTeams.count()  

    # pull individuals with role in 'Press','ICJ','officer','Security Council'
    advisorIndividuals = Delegate.objects.filter(school=advisor.school,
                                                 role__in=['Press','ICJ','officer','Security Council'])
    advisorIndvidualsCount = advisorIndividuals.count() 

    # return HttpResponse('individual ' + str(advisorIndvidualsCount) )
    
    return render(request, 'display_advisor_delegation.html',
                           {'advisor': advisor,
                            'teams': advisorTeams,
                            'teamCount': advisorTeamsCount,
                            'individuals':advisorIndividuals,
                            'invidualCount':advisorIndvidualsCount
                           })  
    
