import React from 'react';
import Question from '../Question/Question'

class QuestionList extends React.Component {
	constructor(props) {
		super(props);
		var arr = []
		for (var i = 0; i < this.props.questions.length; i++) {
			arr.push({
				question_pk : '1',
				answer: ''
			})
		}
		this.state = {
			submitted: false,
			submitted_time: '',
			answers : arr
		}
		// alert(this.props.questions.length)
	}

	st = (temp) => {
		this.setState({
			answers:temp 
		});
	}
	onSubmit = () =>{
		// alert(this.state.answers)
		fetch('http://127.0.0.1:8000/quiz/make/submission/', {
	      method: 'post',
	      headers: {
	        'Content-Type': 'application/json',
	        'Authorization': this.props.token
	      },
	      body: JSON.stringify({
	      	course_pk : this.props.course_pk,
	      	quiz_pk : this.props.quiz_pk,
	      	ques_response: this.state.answers
	      })
	    })
	    .then(response => {return response.json()})
	    .then(response => {
	    	if(response.message==="Succesully submitted the quiz response")
		    	alert("Successfully Submitted!")
		    else
		    	throw new Error(response.message)
	    })
	    .catch(error=> {
	    	alert(error)
	    })
		this.props.onRouteChange('CoursePage')
	}

	onChangeAnswer = (idx, ans) => {
		let temp = [];
		var x;
		if (this.props.questions[idx].question_type==='F') {
			x=ans
		}
		else{
			x = Array.from(ans)
		}
		// alert(x)
		// alert(this.state.answers.length)
		for (var i = 0; i < this.state.answers.length; i++) {
			if(i===idx){
				alert(i)
				temp.push({
					question_pk: this.props.questions[idx].question_pk,
					answer:x
				})
				// alert(this.props.questions[idx].question_pk)
				// alert(x)
				// alert(temp[0].answer)
				// alert(temp)
			}
			else{
				// alert(this.state.answers[i])
				temp.push(this.state.answers[i])
				// alert(temp)
			}
			if(i+1===this.state.answers.length){
				this.st(temp)
			}
		}
		// alert(temp[z].answer)

		
		// alert(this.state.answers[0].answer)
		// alert(temp[0].answer)

	}
	render(){

		const allQuestions = this.props.questions.map((user, i) => {
          return (
            <React.Fragment>
            <Question
              key={i}
              num={i+1}
              question_type={this.props.questions[i].question_type}
              content={this.props.questions[i].content} 
              answer={this.props.questions[i].answer}
              questions={this.props.questions[i]}
              positive_marks={this.props.questions[i].positive_marks}
              negative_marks={this.props.questions[i].negative_marks}
              onChangeAnswer = {this.onChangeAnswer}
              score={this.props.questions[i].your_score}
              score_vis = {this.props.questions[i].your_score_visible}
              user_answer_vis = {this.props.questions[i].user_answer_visible}
              user_answer = {this.props.questions[i].user_answer}
              correct_answer_vis = {this.props.questions[i].correct_answer_visible}
              correct_answer = {this.props.questions[i].correct_answer}
              />
              </React.Fragment>
          );
        });

		return (
			<div>
				<h1 className="f1  garamond"> {this.props.quiz.quiz_title} </h1>
				{allQuestions}
				<div className="w-100 center">
				{
					this.props.show_submit_button 
					? <button class="center f6 link pointer br1 fr mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" onClick={this.onSubmit}> Submit </button>
					: <div />
				}</div>
			</div>
		);
	}


}

export default QuestionList;