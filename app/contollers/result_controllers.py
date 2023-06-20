class ResultController:
    @staticmethod
    async def return_answer_message_text(client_poll_data: dict, poll_data: dict) -> str:
        list_data = []
        for question, answer in client_poll_data.items():
            question_text = poll_data.get(question)['question']
            if poll_data.get(question)['multiple']:
                list_multiple = []
                for one_answer in answer:
                    list_multiple.append(f"{poll_data.get(question)['answers'][one_answer]}\n")
                list_data.append(f'{question_text}\n{"".join(list_multiple)}\n\n')
            else:

                answer_text = poll_data.get(question)['answers'][answer]
                list_data.append(f'{question_text}\n{answer_text}\n\n')

        return ''.join(list_data)

    @staticmethod
    async def return_answer_data(poll_changing: str, question_client: str, data: dict) -> tuple[bool, dict, bool, dict]:
        multiple = False
        branching = False
        for key, data_value in data.items():
            if data_value['question'] == question_client:
                if data_value['branching']:
                    data_for_cache = {}
                    data_answers = {}
                    branching = True
                    return multiple, data_for_cache, branching, data_answers
                key_question = key
                data_answers = data_value['answers']
                data_for_cache = {
                    'poll': poll_changing,
                    'key_question': key_question,
                    'data_answers': data_answers,
                }
                multiple = data_value['multiple']
                break
        return multiple, data_for_cache, branching, data_answers
