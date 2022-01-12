import pdfminer
from pdfminer.high_level import extract_text
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

def sort_questions(file):
    questions = []
    questionNumber = 0
    questionPages = []
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print(pdfReader.numPages)
    for counter in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(counter)
        text = pageObj.extractText()
        if "(a)" in text:  # not foolproof, but works pretty well for us
            questionPages.append(counter)
            questions.append(text)
            questionNumber += 1
            print(counter)
        elif questionNumber != 0:
            questions[questionNumber - 1] = questions[questionNumber - 1] + text
    pdfFileObj.close()
    questionPages.append(pdfReader.numPages)
    return (questions,questionPages)

def find_keywords(arr, keyword):
    question_number = 0
    questions = []
    for question in arr:
        print(question)
        question_number += 1
        if keyword in question:
            questions.append(question_number)
    return questions


def sort_answers(file):
    answers = []
    answerNumber = 0
    answerPages = []
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print(pdfReader.numPages)
    for counter1 in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(counter1)
        text = pageObj.extractText()
        #print(text)
        split_text = text.split()
        counter = 0
        question_counter = 0
        for counter in range(len(split_text)):
            if split_text[counter] == "Marks":
                if "(a)" in split_text[counter+1]:
                    answerPages.append(counter1)
                    answers.append(text)
                    answerNumber += 1
                elif answerNumber!=0:
                    answers[answerNumber-1] = answers[answerNumber-1] + text

    pdfFileObj.close()
    answerPages.append(pdfReader.numPages)
    return (answers,answerPages)


def create_pdf_question(arr,questions,file):
    input_pdf = PdfFileReader(file)
    print(arr)
    for number in questions:
        output = PdfFileWriter()
        print(number)
        for counter in range(arr[number-1],arr[number]):
            output.addPage(input_pdf.getPage(counter))
        with open(file[:-4] + "question_" + str(number) + ".pdf", "wb") as output_stream:
            output.write(output_stream)

def create_pdf_answer(arr,questions,file):
    input_pdf = PdfFileReader(file)
    print(arr)
    for number in questions:
        output = PdfFileWriter()
        print(number)
        for counter in range(arr[number-1],arr[number]):
            output.addPage(input_pdf.getPage(counter))
        with open(file[:-4] + "answer_" + str(number) + ".pdf", "wb") as output_stream:
            output.write(output_stream)

answers,answerPages = sort_answers('/Users/dhruvroongta/Downloads/0620_s20_ms_41.pdf')
print(answers,answerPages)

questions,questionPages = sort_questions('/Users/dhruvroongta/Downloads/0620_s20_qp_41.pdf')
question_numbers = find_keywords(questions,"acids")
create_pdf_question(questionPages,question_numbers,'/Users/dhruvroongta/Downloads/0620_s20_qp_41.pdf')
print(answers,answerPages)
create_pdf_answer(answerPages,question_numbers,'/Users/dhruvroongta/Downloads/0620_s20_ms_41.pdf')


