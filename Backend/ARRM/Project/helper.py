from .models import ProjectTask, ProjectTaskAssignment, ProjectTeam, Milestone
from Profile.models import ResearchAssistant, ResearchAssistantAvailability, Degree, FacultyInterests


REQUIRED_WEEKLY_HOURS = 40
TOTAL_MATCH_SCORE = 7


PROJECT_MILESTONE_TEMPLATE_DICT = {
    "project_planning": [
        "Admin & Project Management",
        "Reporting",
        "IRB application"
    ],

    "literature_review": [
        "Literature review"
    ],

    "data_collection_and_processing": [
        "Development of interview guide for Employers",
        "Development of data collection instruments",
        "Finalisation of research instrument",
        "Review of Instrument",
        "Piloting of instruments",
        "Post-Pilot Update of instruments",
        "Administration of instruments",
        "Data cleaning and processing",
        "Data analysis"
    ],

    "dissemination": [
        "Manuscript development",
        "Pitch design services",
        "Presentation preparation for conference",
        "Manuscript proofreading services",
        "Review of Manuscript",
        "Publication of manuscript"
    ]
}


def get_milestone_dict():
    milestones = Milestone.objects.all()
    MILESTONE_DICT = dict()

    for milestone in milestones:
        milestone_name = milestone.name.lower().replace(" ", "_")
        MILESTONE_DICT[milestone_name] = milestone.name

    return MILESTONE_DICT


def get_cumulative_task_hours(project):
    cumulative_task_hours = 0
    project_tasks = ProjectTask.objects.filter(project_milestone__project=project)

    for project_task in project_tasks:
        if project_task.hours_required:
            cumulative_task_hours += project_task.hours_required

    return cumulative_task_hours


def get_ra_available_hours(ra=None):
    ra_hours = dict()

    if ra:
        ra_total_hours = get_ra_total_hours(ra)
        ra_project_hours = get_ra_project_hours(ra)
        ra_hours[ra.user.id] = ra_total_hours - ra_project_hours

    else:
        ras = ResearchAssistant.objects.all()
        ra_hours = dict()

        for ra in ras:
            # if not ProjectTeam.objects.filter(project=project, user=ra.user).exists():
            ra_total_hours = get_ra_total_hours(ra)
            ra_project_hours = get_ra_project_hours(ra)
            ra_hours[ra.user.id] = ra_total_hours - ra_project_hours 

    return ra_hours

    
def get_ra_total_hours(ra):
    ra_availability = ResearchAssistantAvailability.objects.filter(ra=ra)
    ra_total_hours = 0
    for availability in ra_availability:
        semester = availability.semester
        semester_weeks = (semester.end_date - semester.start_date).days
        
        # offset semester weeks by 2 to account for mid-semester and exam weeks
        semester_weeks -= 2
        ra_total_hours += semester_weeks * REQUIRED_WEEKLY_HOURS

    return ra_total_hours


def get_ra_project_hours(ra):
    project_team = ProjectTeam.objects.filter(user=ra.user)
    total_project_hours = 0

    for team in project_team:
        assigned_tasks = ProjectTaskAssignment.objects.filter(project_task__project_milestone__project=team.project, assignee=ra.user)
        project_hours = 0

        for assigned_task in assigned_tasks:
            if assigned_task.project_task.hours_required:
                project_hours += assigned_task.project_task.hours_required
        
        total_project_hours += project_hours

    return total_project_hours


def get_available_ras(ra_available_hours, project, assigned_project_hours):
    available_ras = list()
    for ra_id, hours in ra_available_hours.items():
        # removed assigned task hours from estimated project hours
        if hours - (project.estimated_project_hours - assigned_project_hours) >= 0:
            available_ras.append(ra_id)

    return available_ras


def compute_project_study_area_match_score(ra, project_study_areas):
    matching_score = 0
    total_score = 0
    study_areas = set(interest["study_area"] for interest in ra["interests"])

    for area in project_study_areas:
        if area in study_areas:
            matching_score += 1
        total_score += 1

    return (matching_score / total_score) * 3


def compute_faculty_study_area_match_score(ra, faculty):
    matching_score = 0
    total_score = 0
    ra_study_areas = set(interest["study_area"] for interest in ra["interests"])
    faculty_study_areas = set(interest.interest.study_area for interest in FacultyInterests.objects.filter(faculty=faculty))

    for area in ra_study_areas:
        if area in faculty_study_areas:
            matching_score += 1
        total_score += 1

    return (matching_score / total_score) * 2


def compute_interest_match_score(ra, project):
    matching_score = 0
    total_score = 0

    interests = set(interest["name"] for interest in ra["interests"])
    interests_set = set()

    for interest in interests:
        interest_set = set(interest.lower().split())
        interests_set = interests_set.union(interest_set)
    
    for interest in interests_set:
        if interest in project.description.lower():
            matching_score += 1
        
        if interest in project.title.lower():
            matching_score += 1

        total_score += 2

    return (matching_score / total_score) * 1


def compute_degree_match_score(ra, project):
    matching_score = 0
    total_score = 0

    faculty_degrees = list(degree.major for degree in Degree.objects.filter(user=project.user))

    if faculty_degrees:
        ra_degrees = list(degree["major"] for degree in ra["degrees"]) 
        for degree in ra_degrees:
            if degree in faculty_degrees:
                matching_score += 1
                total_score += 1
        
        if total_score > 0:
            return (matching_score / total_score) * 1

    return 0