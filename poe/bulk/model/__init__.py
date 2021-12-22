"""
Copyright (c) 2019-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from .model import Model
from .modules.feature_extraction import VGG_FeatureExtractor


def feature_extraction_factory(feature_extraction_type:str,input_channel:int,output_channel:int):
    cls={
        'VGG':VGG_FeatureExtractor,
    }
    return cls[feature_extraction_type](input_channel,output_channel)




