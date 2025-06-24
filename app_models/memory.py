class Memory:
    __instance = None
    es_helper = None
    indexes = {}

    @staticmethod
    def get_instance():
        """
        Get the permanent state of the memory.

        :return: The Memory instance.
        """
        if Memory.__instance is None:
            Memory()
        return Memory.__instance

    def __init__(self):
        """
        Virtual private constructor.
        """
        if Memory.__instance is not None:
            raise Exception("This class is a singleton !")
        else:
            Memory.__instance = self
