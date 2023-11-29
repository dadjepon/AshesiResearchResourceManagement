def transcript_upload_path(instance, filename):
    """
    defines upload path for degree transcript

    Args:
        - instance: instance of degree model
        - filename: name of file

    Returns:
        - path: path to upload transcript
    """

    username = instance.user.email.split("@")[0]
    return f"transcripts/{username}/{filename}"


def sample_upload_path(instance, filename):
    """
    defines upload path for writing sample

    Args:
        - instance: instance of writing sample model
        - filename: name of file

    Returns:
        - path: path to upload writing sample
    """

    username = instance.user.email.split("@")[0]
    return f"samples/{username}/{filename}"


def profile_picture_upload_path(instance, filename):
    """
    defines upload path for profile picture

    Args:
        - instance: instance of profile picture model
        - filename: name of file

    Returns:
        - path: path to upload profile picture
    """

    username = instance.user.email.split("@")[0]
    return f"profile_pictures/{username}_{filename}"


def cv_upload_path(instance, filename):
    """
    defines upload path for cv

    Args:
        - instance: instance of cv model
        - filename: name of file

    Returns:
        - path: path to upload cv
    """

    username = instance.user.email.split("@")[0]
    return f"cvs/{username}_{filename}"