from .status import Status


class Process:
    """
    Job will have one or more processes.
    """
    def __init__(self, id=None, name=None, status=Status.WAITING, is_active=False):
        self.id = id
        self.name = name
        self.status = status
        self.is_active = is_active
        self.previous_status = None

    def change_status_to(self, status):
        if not self.is_active:
            raise Exception('Can not change status of inactive process')
        if status.value < self.status.value:
            raise Exception('Can not change status from ' + status.name + ' to ' + self.status.name)
        self.previous_status = self.status
        self.status = status

    def resume(self):
        if not self.is_active:
            raise Exception('Can not change status of inactive process')
        if not self.status == Status.HOLD:
            raise Exception('Can not resume the process. Not a hold process.')
        self.status = self.previous_status

    def update_status(self):
        if not self.is_active:
            raise Exception('Can not change status of inactive process')
        if self.status == Status.FAILED or self.status == Status.COMPLETED:
            raise Exception('Can not change status of ' + self.status.name + ' process')
        if self.status == Status.HOLD:
            raise Exception('Can not change status of ' + self.status.name + ' process. Resume the process first.')
        self.previous_status = self.status
        self.status = Status(self.status.value + 1)
        if self.status == Status.COMPLETED or self.status == Status.FAILED:
            self.is_active = False

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.name,
            "previous_status": self.previous_status.name if self.previous_status is not None else None,
            "is_active": self.is_active
        }

    @staticmethod
    def create_processes_from_string_list(process_list):
        processes = []
        for index, process_name in enumerate(process_list):
            processes.append(Process(id=index, name=process_name))
        return processes
