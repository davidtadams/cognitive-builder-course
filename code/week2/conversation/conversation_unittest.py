import unittest
#from unittest.mock import patch
import unittest.mock as mock

import json

def parse_json_string(json_string):
    json_data = json.loads(json_string)
    return(json_data)

import conversation_prompt


class ConversationMock():
    mock_input_list = [    "Hi I'd like to get in touch with someone",
                           "Jeff",
                           "q"
                       ]
    mock_input_index = 0

    def __init__(self):
        self.kwargs_list = []
        self.mock_responses = []
        self.mock_iteration = 0

    def fill_mock_responses(self):
        json_string = b"""{"intents": [], "entities": [], "input": {}, "output": {"log_messages": [], "text": ["Hello, how may I help you?"], "nodes_visited": ["Start"]}, "context": {"conversation_id": "5067da89-d43f-4ec7-b029-b4e864571b61", "system": {"dialog_stack": [{"dialog_node": "root"}], "dialog_turn_counter": 1, "dialog_request_counter": 1, "_node_output_map": {"Start": [0, 1, 0]}, "branch_exited": true, "branch_exited_reason": "completed"}}, "alternate_intents": false}"""
        json_response = parse_json_string(json_string)
        self.mock_responses.append(json_response)

        json_string = b"""{"intents": [{"intent": "getincontact", "confidence": 1}], "entities": [{"entity": "hello", "location": [0, 2], "value": "Hello", "confidence": 1}], "input": {"text": "Hi I'd like to get in touch with someone."}, "output": {"log_messages": [], "text": ["Can you tell me who you're trying to contact?"], "nodes_visited": ["Contacting", "No contact specified."]}, "context": {"conversation_id": "5067da89-d43f-4ec7-b029-b4e864571b61", "system": {"dialog_stack": [{"dialog_node": "No contact specified."}], "dialog_turn_counter": 2, "dialog_request_counter": 2, "_node_output_map": {"Start": [0, 1, 0], "No contact specified.": [0]}}}, "alternate_intents": false}"""
        json_response = parse_json_string(json_string)
        self.mock_responses.append(json_response)

        json_string = b"""{"intents": [{"intent": "getincontact", "confidence": 1}], "entities": [{"entity": "sys-person", "location": [0, 4], "value": "Jeff", "confidence": 0.998245}], "input": {"text": "Jeff"}, "output": {"log_messages": [], "text": ["Let me look for Jeff..."], "nodes_visited": ["Contact Specified"], "action": {"search_person": "Jeff"}}, "context": {"conversation_id": "5067da89-d43f-4ec7-b029-b4e864571b61", "system": {"dialog_stack": [{"dialog_node": "root"}], "dialog_turn_counter": 3, "dialog_request_counter": 3, "_node_output_map": {"Start": [0, 1, 0], "No contact specified.": [0], "node_27_1494198422393": [0]}, "branch_exited": true, "branch_exited_reason": "completed"}}, "alternate_intents": false}"""
        json_response = parse_json_string(json_string)
        self.mock_responses.append(json_response)

    def message(self, **kwargs):
        #print("kwargs: {}".format(kwargs))
        self.kwargs_list.append(kwargs)
        #print("mock responses: {}".format(len(self.mock_responses)))
        ret_value = self.mock_responses[self.mock_iteration]
        self.mock_iteration += 1
        return(ret_value)

    @staticmethod
    def input_mock(prompt_str):
        if ConversationMock.mock_input_index < len(ConversationMock.mock_input_list):
            ret_value = ConversationMock.mock_input_list[ConversationMock.mock_input_index]
            ConversationMock.mock_input_index += 1
            #print("input_mock returns {}".format(ret_value))
            return(ret_value)
        else:
            raise ValueError("Your loop didn't quit.")


class TestChallenge(unittest.TestCase):
    @mock.patch('builtins.input', side_effect=ConversationMock.input_mock)
    def test_main_loop(self, mockinput):
        mock_obj = ConversationMock()
        mock_obj.fill_mock_responses()

        conversation_prompt.main_loop(mock_obj, "workspace_whatever")

        # warning: iteration 0 has no context
        for i in range(1, mock_obj.mock_iteration):
            self.assertTrue("context" in mock_obj.kwargs_list[i], "when calling message() you should provide a 'context' keyword argument")
            self.assertTrue(type(mock_obj.kwargs_list[i]["context"]) is dict, "context argument should be a dict")
            self.assertTrue("conversation_id" in mock_obj.kwargs_list[i]["context"], "context argument dictionary should contain conversation_id key")
