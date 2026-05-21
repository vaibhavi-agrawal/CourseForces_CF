import React from 'react';

const QuizInfoPage = (props) => {
	return (
		<div> 
			<h2 className="center f2 underline black"> {props.quiz.quiz_title} </h2>
			<header className="bg-light-yellow sans-serif w-50 center">
				<div className="mw9 center pa4 ph7-l">
				<h4 className="f3 fw1 georgia i">
				{props.quiz.content}
				</h4>
				</div>
			</header>
				<h4 className="f4 fw1 georgia i">
				Start Time: {props.quiz.start_at}
				</h4>
				<h4 className="f4 red fw1 georgia i">
				Deadline: {props.quiz.deadline}
				</h4>
			<div className="w-50 center ma2 pa2">
				<button onClick = {() => props.loadQuestions()} className="f6 link pointer br1 fr mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" > {
					props.role==='P'
					? "View Quiz" : 
					props.quiz.show_total_score
					? "View Result"
					: "Take Quiz!"
				} </button>
				{
					props.role === 'P'
					?  <div >
							{
							props.ans_vis 
							? <button onClick = {() => props.loadMarkList()} className="f6 link pointer br1 fr mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" > View Marks List</button>
							: <button onClick = {() => props.checkQuiz()} className="f6 link pointer br1 fr mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" > Check Quiz</button>
								
							}
					   </div>
					:  <div />
				}
			</div>
			{
			    props.role==='P'
			    ? <div className = "w-100 mt4 pa2 flex">
			    <button class="f6 link pointer br1 center fr ph4 pv3 mb2 shadow-4 dib white bg-red" onClick = {() => props.deleteQuiz()}  >Delete Quiz</button>
			    </div>
			    : <div />
		  }
		</div>
	);
} 

export default QuizInfoPage;