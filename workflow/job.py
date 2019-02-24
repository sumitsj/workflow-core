from .process import Process
from .status import Status
import json

class Job:
    """
    Job in workflow.
    """
    def __init__(self, id=None, name=None, process_list=[]):
        self.id = id
        self.name = name
        self.processes = Process.create_processes_from_string_list(process_list)

    
    def start(self):
        self.__raise_exception_if_process_list_is_empty()
        
        self.processes[0].is_active = True
        self.processes[0].update_status()

    def update_job(self):
        self.__raise_exception_if_update_requested_for_failed_job()

        active_process = next((process for process in self.processes if process.is_active), None)
        if active_process is None:
            active_process = next((process for process in self.processes if process.status == Status.WAITING), None)
            if active_process is None:
                self.__raise_exception_if_update_requested_for_completed_job()
            active_process.is_active = True

        active_process.update_status()

    def abort(self):
        active_process = next((process for process in self.processes if process.is_active), None)
        if active_process is not None:
            active_process.change_status_to(Status.FAILED)

    def put_on_hold(self):
        active_process = next((process for process in self.processes if process.is_active), None)
        if active_process is not None:
            active_process.change_status_to(Status.HOLD)

    def resume(self):
        active_process = next((process for process in self.processes if process.is_active), None)
        if active_process is not None:
            active_process.resume()

    def to_json(self):
        dict_representation = {
            "id": self.id,
            "name": self.name,
            "processes": [process.to_json() for process in self.processes]
        }
        return json.dumps(dict_representation, default=lambda o: o.__dict__, indent=4)
    
    @staticmethod
    def parse(str):
        job_dict = json.loads(str)
        job = Job(id=job_dict["id"], name=job_dict["name"])
        job.processes = Process.parse(job_dict["processes"])
        return job

    def __raise_exception_if_process_list_is_empty(self):
        if(len(self.processes) == 0):
            raise Exception("Process list is empty")

    def __raise_exception_if_update_requested_for_failed_job(self):
        active_process = next((process for process in self.processes if process.is_active), None)
        if(active_process and active_process.status == Status.FAILED):
            raise Exception("Can not update status of FAILED job")

    def __raise_exception_if_update_requested_for_completed_job(self):
        raise Exception("Can not update status of COMPLETED job")
