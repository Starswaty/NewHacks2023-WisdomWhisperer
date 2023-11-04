import { useState } from "react";
import { Button } from "@/components/ui/button";

function QuizQuestion({ question, answerArr, id, correctAns }) {
  const [correct, setCorrect] = useState(false);
  const [selectionArr, setSelectionArr] = useState(() => Array(answerArr.length).fill(false));

  const handleSelection = (index) => {
    const newSelectionArr = Array(answerArr.length).fill(false);
    newSelectionArr[index] = true;
    setSelectionArr(newSelectionArr);
  }

  return (
    <>
      <div className="flex flex-col space-y-2">
        <h2 className="text-xl font-bold text-black dark:text-white">
          Question {id}
        </h2>
        <p className="text-base text-gray-600 dark:text-gray-300">{question}</p>
        {answerArr.map((answer, index) => (
          <div
            className={`flex flex-row rounded-md border items-center p-4 gap-4 ${
              selectionArr[index] ? 'border-blue-500' : 'border-gray-300'
            }`}
            key={index}
            onClick={() => handleSelection(index)}
          >
            <label>
              {answer}
            </label>
          </div>
        ))}
        <Button type="button" variant="outline">
          Check Answer
        </Button>
      </div>
    </>
  );
}

export default QuizQuestion;