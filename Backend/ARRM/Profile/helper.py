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