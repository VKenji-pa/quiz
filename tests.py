import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
#############

#1
def test_init_choice_check():
    question = Question(title="test")

    assert len(question.choices) == 0

#2    
def test_create_invalid_choice():
    question = Question(title="test")
    
    with pytest.raises(Exception):
        question.add_choice("")
    with pytest.raises(Exception):
        question.add_choice("a"*101)
    with pytest.raises(Exception):
        question.add_choice("a"*300)    

#3
def test_incremental_choice_id():
    question = Question(title="test")
    
    for i in range(10):
        question.add_choice("a"*(i+1), False)
        
    question.add_choice("final", True)
    
    for i in range(10):
        question.remove_choice_by_id(i+1)
    
    choice = question.choices[0]
    assert choice.id == 11

#4
def test_select_non_existent_id():
    question = Question(title="test")
    
    question.add_choice("A", True)
    question.add_choice("B", True)
    question.add_choice("C", False)
    
    with pytest.raises(Exception):
        question._choice_by_id(4) 
  
#5      
def test_remove_all_choices():
    question = Question(title="test")
    
    question.add_choice("A", True)
    question.add_choice("B", True)
    question.add_choice("C", False)

    question.remove_all_choices()
    
    assert len(question.choices) == 0

#6
def test_remove_choice_by_id():
    question = Question(title="test")
    
    question.add_choice("A", True)
    question.add_choice("B", True)
    question.add_choice("C", False)
    
    question.remove_choice_by_id(2)
    
    assert len(question.choices) == 2
    with pytest.raises(Exception):
        question._choice_by_id(2)

#7 
def test_selection_limit():
    question = Question(title="test")
    
    question.add_choice("A", True)
    question.add_choice("B", False)
    question.add_choice("C", False)
    
    with pytest.raises(Exception):
        question.select_choices([1, 2])

#8  
def test_multi_select_all_correct_choices():
    question = Question(title="test", max_selections=50)
    ids = []
    
    for i in range(50):
        ids.append(i+1)
        if i % 2 == 0:
            question.add_choice("t", True)
        else:
            question.add_choice("f", False)
    
    correct = question.select_choices(ids)
    
    assert len(correct) == 25
    assert correct[-1] == 49

#9    
def test_try_set_empty_question_as_correct():
    question = Question(title="test")
    
    with pytest.raises(Exception):
        question.set_correct_choices([1])

#10      
def test_set_all_choices_to_correct():
    question = Question(title="test", max_selections=10)
    ids = []
    
    for i in range(10):
        ids.append(i+1)
        question.add_choice("a"*(i+1), False)
        
    selected = question.select_choices(ids)
    assert len(selected) == 0
    
    question.set_correct_choices(ids)
    selected = question.select_choices(ids)
    assert len(selected) == 10