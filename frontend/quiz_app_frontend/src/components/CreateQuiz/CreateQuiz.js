import React from 'react';

class CreateQuiz extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      num_of_questions: 0,
      title: '',
      content: '',
      deadline: '',
      start_at: '',
    }
  }

  onTitleChange = (event) => {
  	this.setState({title: event.target.value})
  }
  onContentChange = (event) => {
  	this.setState({content: event.target.value})
  }

  onStartChange = (event) => {
  	this.setState({start_at: event.target.value})
  }

  onEndChange = (event) => {
  	this.setState({deadline: event.target.value})
  }

  onTotalChange = (event) => {
  	this.setState({num_of_questions: Number(event.target.value)})
  }

  onSubmit = () => {
  	// Send to backend, route to CreateQuestions
  	// alert("Here!")
	fetch('http://127.0.0.1:8000/quiz/add/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': this.props.token
      },
      body: JSON.stringify({
      	title : this.state.title,
      	content: this.state.content,
      	course_pk : this.props.course_pk,
      	deadline: this.state.deadline,
      	start_at: this.state.start_at
      })
    })
      .then(response => {
      	// alert(response)
      	return response.json()
      })
      .then(data => {
      	// Save quiz pk info in App.js
      	if(data.message === "Successfully created Quiz!"){
      		alert(data.message)
      		this.props.setQuiz(data.quiz_pk, this.state.num_of_questions)
		  	this.props.onRouteChange("CreateQuestions")
      	}
      	else
      		throw new Error(data.message)
      })
      .catch(error => {
      	alert(error)
      })
  }
  render() {
  	return (
  		<div>
			<div className="gray f2 serif"> Create New Quiz </div>
			<div class="db center mw5 mw6-ns hidden br2 shadow-5 ">
			<div className="w-100">
				<h3 className="f4 bold serif">Title: <input id="title" className="dib ml5 mt2 input-reset ba b--black-20 pa2 mb2 db w-50"
	  			type="text"
	  			onChange={this.onTitleChange}
				/> </h3>
			</div>
			<div className="w-100">
				<h3 className="f4 mr2 dib serif">Content: </h3> <textarea id="content" className="dib mt2 ml4 input-reset ba b--black-20 pa2 mb2 db w-50"
	  			onChange={this.onContentChange}
	  			type="text"
				/> 
			</div>
			<div className="w-100">
				<h3 className="f4 bold serif">Start time: <input id="start_at" className="dib ml2 input-reset ba b--black-20 pa2 mb2 db w-50"
	  			type="text"
	  			onChange={this.onStartChange}
				/> </h3>
			</div>
			<div className="w-100">
				<h3 className="f4 bold serif">End time: <input id="deadline" className="dib ml2 input-reset ba b--black-20 pa2 mb2 db w-50"
	  			type="text"
	  			onChange={this.onEndChange}
				/> </h3>
			</div>
			<div className="w-100">
				<h3 className="f4 bold serif">Total Questions: <input onKeyPress={(event) => {if (!/[0-9]/.test(event.key)) {event.preventDefault();}}} id="num_of_questions" className="dib ml2 input-reset ba b--black-20 pa2 mb2 db w-50"
	  			onChange={this.onTotalChange}
				/> </h3>
			</div>	
			<button className="f6 link pointer br1  mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" onClick = {() => this.onSubmit()}> Add Questions </button>
		</div>
  		</div>
  	);
  }
}

export default CreateQuiz;