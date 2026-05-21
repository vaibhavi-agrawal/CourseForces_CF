import React from 'react';

class Question extends React.Component {
  constructor(props){
  	super(props);
  	this.state= {
  		checked_radio_option: '',
  		checkbox_options: new Set(),
  		true_false: '',
  		subjective: ''
  	}
  }

  onClickRadio = (event) => {
  	var c = this.state.checked_radio_option
  	this.setState({
  		checked_radio_option: c===Number(event.target.id) ? '':Number(event.target.id)
  	});

  	this.props.onChangeAnswer(this.props.num-1, [Number(event.target.value)]);
  }

  onClickCheck = (event) => {
  	var s = this.state.checkbox_options;
  	var x = Number(event.target.value);
  	if(s.has(x)){
  		s.delete(x)
  	}
  	else{
  		s.add(x)
  	}
  	var ans= s
  	this.setState({
  		checkbox_options:s 
  	});

  	this.props.onChangeAnswer(this.props.num-1, ans );
  }

  // onClickTF = (event) => {
  // 	var c = this.state.true_false
  // 	var ans = c===event.target.value ? '': event.target.value
  // 	this.setState({
  // 		true_false: c===event.target.value ? '': event.target.value
  // 	});
  // 	this.props.onChangeAnswer(this.props.num-1, ans );
  // }

  	onChangeSub = (event) => {

  		this.setState({
  			subjective:event.target.value 
  		});
	  	this.props.onChangeAnswer(this.props.num-1, event.target.value);
  	}

  

  render(){

	  return (
	  	<div>
		    <div className='flex flex-column w-75 center tc bg-light-yellow br3 pa3 ma3 dib bw2 shadow-5'>
		      <h2 className="serif f3"> Question #{this.props.num}: {this.props.content} </h2>
		      <h4 className="f4 red mt0 i garamond" > Positive Score: {this.props.positive_marks}, Negative Score: {this.props.negative_marks} {this.props.score_vis? `, Your Score: ${this.props.score}`:``} </h4>
		      {
		      	this.props.question_type==='S'
		      	? <div>
					<form class="center pa2 flex flex-column">
					    <div class="flex items-center w-100 mb2">
					      <input class="mr2 ml4" onChange={this.onClickRadio} type="checkbox" checked={this.state.checked_radio_option===1} id={1} value={this.props.questions.options[0].option_pk} />
					      <label class="serif pl3 f4 i lh-copy">{this.props.questions.options[0].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickRadio} class="mr2 ml4" type="checkbox" checked={this.state.checked_radio_option===2} id={2} value={this.props.questions.options[1].option_pk} />
					      <label class="f4 pl3 i serif lh-copy">{this.props.questions.options[1].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickRadio} class="mr2 ml4" type="checkbox" checked={this.state.checked_radio_option===3} id={3} value={this.props.questions.options[2].option_pk} />
					      <label  class="f4 i pl3 serif lh-copy">{this.props.questions.options[2].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickRadio} class="mr2 ml4" type="checkbox" checked={this.state.checked_radio_option===4} id={4} value={this.props.questions.options[3].option_pk} />
					      <label class="f4 i pl3 serif lh-copy">{this.props.questions.options[3].option_value}</label>
					    </div>
					</form>
		      	</div>
		      	: this.props.question_type==='M'
		      	? <div>
		      		<form class="center pa2 flex flex-column">
					    <div class="flex items-center w-100 mb2">
					      <input class="mr2 ml4" onChange={this.onClickCheck} type="checkbox" id={1}  value={this.props.questions.options[0].option_pk} />
					      <label class="serif pl3 f4 i lh-copy">{this.props.questions.options[0].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickCheck} class="mr2 ml4" type="checkbox" id={2}  value={this.props.questions.options[1].option_pk} />
					      <label class="f4 pl3 i serif lh-copy">{this.props.questions.options[1].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickCheck} class="mr2 ml4" type="checkbox" id={3}  value={this.props.questions.options[2].option_pk} />
					      <label  class="f4 i pl3 serif lh-copy">{this.props.questions.options[2].option_value}</label>
					    </div>
					    <div class="flex items-center w-100 mb2">
					      <input onChange={this.onClickCheck} class="mr2 ml4" type="checkbox" id={4}  value={this.props.questions.options[3].option_pk} />
					      <label class="f4 i pl3 serif lh-copy">{this.props.questions.options[3].option_value}</label>
					    </div>
					</form>
		      	 </div>
		      	: this.props.question_type==='F'
		      	?  <textarea id="comment" onChange={this.onChangeSub} class="db center border-box hover-black w-100 measure ba b--black-20 pa2 br2 mb2" aria-describedby="comment-desc"></textarea>
		      	: <h2 className="red"> Invalid Question Type!</h2>
		      }
		    {
		    	this.props.user_answer_vis
		    	? <h4 > Your answer: {this.props.user_answer} </h4>
		    	: <div />
		    }
		    {
		    	this.props.correct_answer_vis
		    	? <h4 className="green "> Correct answer: {this.props.correct_answer} </h4>
		    	: <div />
		    }
		    </div>
	    </div>
	  );
	}
}

export default Question;