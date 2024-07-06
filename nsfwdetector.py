from nudenet import NudeClassifier
classifier = NudeClassifier()

def is_nsfw(image_path):
    """Returns True if detects NSFW content"""
    data = classifier.classify(image_path)
    peak = 0.69
    if float(data[image_path]["safe"]) < peak:
        return True
    else: return False