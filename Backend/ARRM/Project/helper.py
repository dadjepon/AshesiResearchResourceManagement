from .models import ProjectTask, ProjectTeam
from Profile.models import ResearchAssistant, ResearchAssistantAvailability


REQUIRED_WEEKLY_HOURS = 40

MILESTONE_DICT = {
    "project_planning": "Project Planning",
    "literature_review": "Literature Review",
    "data_collection_and_processing": "Data Collection and Processing",
    "dissemination": "Dissemination"
}

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

def get_cummulative_task_hours(project):
    cummulative_task_hours = 0
    project_tasks = ProjectTask.objects.filter(project_milestone__project=project)

    for project_task in project_tasks:
        if project_task.hours_required:
            cummulative_task_hours += project_task.hours_required

    return cummulative_task_hours

def get_ra_available_hours(project):
    ras = ResearchAssistant.objects.all()
    ra_hours = dict()

    for ra in ras:
        # if not ProjectTeam.objects.filter(project=project, user=ra.user).exists():
        ra_total_hours = get_ra_total_hours(ra)
        ra_project_hours = get_ra_project_hours(ra)
        ra_hours[ra.user.id] = ra_total_hours - ra_project_hours # type: ignore 

    return ra_hours
    
def get_ra_total_hours(ra):
    ra_availability = ResearchAssistantAvailability.objects.filter(ra=ra)
    ra_total_hours = 0
    for availability in ra_availability:
        semester = availability.semester
        semester_weeks = (semester.end_date - semester.start_date).days
        
        # offset semester weeks by 2 to account for midsem and exam weeks
        semester_weeks -= 2
        ra_total_hours += semester_weeks * REQUIRED_WEEKLY_HOURS

    return ra_total_hours

def get_ra_project_hours(ra):
    project_team = ProjectTeam.objects.filter(user=ra.user)
    total_project_hours = 0

    for team in project_team:
        project_tasks = ProjectTask.objects.filter(project_milestone__project=team.project, assignee=ra.user)
        project_hours = 0

        for project_task in project_tasks:
            if project_task.hours_required:
                project_hours += project_task.hours_required
        
        total_project_hours += project_hours

    return total_project_hours

def get_available_ras(ra_available_hours, project, assigned_project_hours):
    available_ras = list()
    for ra_id, hours in ra_available_hours.items():
        # removed assigned task hours from estimated project hours
        if hours - (project.estimated_project_hours - assigned_project_hours) >= 0:
            available_ras.append(ra_id)

    return available_ras