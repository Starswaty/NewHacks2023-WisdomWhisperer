import { useState } from 'react'
import QuizQuestion from './components/QuizQuestion'

function App() {

  return (
    <>
      <div className='flex flex-col justify-center items-center gap-4'>
        <QuizQuestion question={"Prove this transformation is linear"} answerArr={["Answer 1", "Answer 2"]} id={1} correctAns={"Answer 2"}/>
      </div>
    </>
  )
}

export default App
