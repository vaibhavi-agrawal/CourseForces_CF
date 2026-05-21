import React from 'react';
import Quiz from '../QuizCard/QuizCard';
import Add from '../Add/Add'

const QuizList = (props) => {
  const allCards = props.quizzes.map((user, i) => {
          return (
            <React.Fragment>
            <Quiz
              onRouteChange={props.onRouteChange}
              key={props.quizzes[i].pk}
              idx={i}
              loadQuizInfo = {props.loadQuizInfo}
              quiz_title={props.quizzes[i].title}
              show_score = {props.quizzes[i].show_total_score}
              score = {props.quizzes[i].total_score}
              />
              </React.Fragment>
          );
        });
  return (

    <div>
    {
        props.quizzes.length===0 && props.role !== 'P'?
        <div >
        <h1 className="ma2 pa4 helvetica f1 green i"> No quizzes to display ...</h1>
        <h1 className="helvetica f1 green i"> Enjoy your day!</h1>
        </div>
        : <div > 
          <h1 className="f1 ml6 mid-gray helvetica"> Quizzes for {props.course_code} {props.role==='P'? <button class="f6 link pointer br1 fr mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" onClick = {() => props.loadStudents()}  >View Course Users</button> : <div />} </h1>
          {allCards}
          {
            props.role==='P'
            ? <Add text="Quiz" onRouteChange={props.onRouteChange} route="CreateQuiz" />
            : <div />
          }
          </div>
  }
  {
    props.role==='P'
    ? <div className = "w-100 mt4 pa2 flex">
    <button class="f6 link pointer br1 center fr mr4 ph4 pv3 mb2 shadow-4 dib white bg-red" onClick = {() => props.deleteCourse()}  >Delete Course</button>
    </div>
    : <div />
  }
  </div>
  );
}

export default QuizList;