from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str
    
# @dataclass
# class DataTransformationArtifact:
#     transformed_train_filepath:str
#     transformed_test_filepath:str
    
