import React from 'react';

class CreateCourse extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      course_code: '',
      course_name: '',
      offered_year: '',
    }
  }

  onCodeChange = (event) => {
    this.setState({course_code: event.target.value})
  }
  onNameChange = (event) => {
    this.setState({course_name: event.target.value})
  }
  onYearChange = (event) => {
    this.setState({offered_year: event.target.value})
  }

  onAdd = () => {
    // Check empty fields and Send info to backend
    fetch('http://127.0.0.1:8000/courses/create/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': this.props.data.token
      },
      body: JSON.stringify({
        course_code : this.state.course_code,
        course_name : this.state.course_name,
        offered_year : this.state.offered_year
      })
    })
      .then(response => {
        if(response.status === 200){
          alert("Course Added Successfully!")
          this.props.loadUser(this.props.data)

        }
        else{
          throw new Error(response)
        }
      })
      .catch(error => {
        alert("Something's wrong, an error occured :(")
        console.log("Error: "+error);
      })
    this.props.onRouteChange('home')
  }
 

  render() {
    return (
      <div>
      <div className="gray f2 serif"> Create New Course </div>
      <div class="db center mw5 mw6-ns hidden br2 shadow-5 ">
      <div className="w-100">
        <h3 className="f4 bold serif">Course Code: <input id="title" className="dib ml2 mt2 input-reset ba b--black-20 pa2 mb2 db w-50"
          type="text"
          onChange={this.onCodeChange}
        /> </h3>
      </div>
      <div className="w-100">
        <h3 className="f4 bold serif">Course Name: <input id="start_at" className="dib ml2 input-reset ba b--black-20 pa2 mb2 db w-50"
          type="text"
          onChange={this.onNameChange}
        /> </h3>
      </div>
      <div className="w-100">
        <h3 className="f4 bold serif">Offered Year: <input
        id="deadline" className="dib ml2 input-reset ba b--black-20 pa2 mb2 db w-50"
          type="text"
          onKeyPress={(event) => {if (!/[0-9]/.test(event.key)) {event.preventDefault();}}}
          onChange={this.onYearChange}
        /> </h3>
      </div>
      <button className="f6 link pointer br1  mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" onClick = {this.onAdd}> Add Course </button>
    </div>
      </div>
    );
  }
}

export default CreateCourse;