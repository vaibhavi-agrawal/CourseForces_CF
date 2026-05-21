import React from 'react';

class Register extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      username: '',
      department: '',
      email: '',
      password: '',
      confirm_password: ''
    }
  }

  onNameChange = (event) => {
    this.setState({name: event.target.value})
  }

  onUserNameChange = (event) => {
    this.setState({username: event.target.value})
  }

  onEmailChange = (event) => {
    this.setState({email: event.target.value})
  }

  onPasswordChange = (event) => {
    this.setState({password: event.target.value})
  }

  onDeptChange = (event) => {
    this.setState({department: event.target.value})
  }

  onCnfPasswordChange = (event) => {
    this.setState({confirm_password: event.target.value})
  }

  
  formatError = (data) => {
    if (typeof data === 'string') return data;
    if (data.message) return data.message;
    return Object.entries(data)
      .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
      .join('\n');
  }

  onSubmitSignIn = () => {
    if (!this.state.department) {
      alert('Please select a department.');
      return;
    }
    fetch('http://127.0.0.1:8000/users/register/', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        name: this.state.name,
        username: this.state.username,
        department: this.state.department,
        email: this.state.email,
        password: this.state.password,
        confirm_password: this.state.confirm_password
      })
    })
      .then(async (response) => {
        const data = await response.json();
        if (response.status === 200) {
          alert(data.message || 'Registered! Check your email to activate your account, then sign in.');
          this.props.onRouteChange('signin');
          return;
        }
        throw new Error(this.formatError(data));
      })
      .catch(error => {
        alert(error.message || "Something's wrong, an error occurred :(");
        console.log(error);
      })
  }

  render() {
    const {onRouteChange} = this.props
    return (
      <article className="br3 ba b--black-10 mv4 w-100 w-50-m w-25-l mw6 shadow-5 center">
        <main className="pa4 black-80">
          <div className="measure">
            <fieldset id="sign_up" className="ba b--transparent ph0 mh0">
              <legend className="f1 fw6 ph0 mh0">Register</legend>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="name">Name</label>
                <input
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="text"
                  name="name"
                  id="name"
                  onChange={this.onNameChange}
                />
              </div>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="name">Username</label>
                <input
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="text"
                  name="name"
                  id="name"
                  onChange={this.onUserNameChange}
                />
              </div>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="department">Department</label>
                <select
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  name="department"
                  id="department"
                  value={this.state.department}
                  onChange={this.onDeptChange}
                >
                  <option value="">Select department</option>
                  <option value="CSE">CSE — Computer Science</option>
                  <option value="MSE">MSE — Material Science</option>
                  <option value="AE">AE — Aerospace</option>
                  <option value="ME">ME — Mechanical</option>
                  <option value="EE">EE — Electrical</option>
                  <option value="MTH">MTH — Mathematics & Computing</option>
                  <option value="BSBE">BSBE — Biological Science & BioEngineering</option>
                  <option value="CHE">CHE — Chemical</option>
                  <option value="CE">CE — Civil</option>
                </select>
              </div>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="email-address">Email</label>
                <input
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="email"
                  name="email-address"
                  id="email-address"
                  onChange={this.onEmailChange}
                />
              </div>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="password">Password</label>
                <input
                  className="b pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="password"
                  name="password"
                  id="password"
                  onChange={this.onPasswordChange}
                />
              </div>
              <div className="mt2">
                <label className="db fw6 lh-copy f6" htmlFor="password">Confirm Password</label>
                <input
                  className="b pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="password"
                  name="password"
                  id="password"
                  onChange={this.onCnfPasswordChange}
                />
              </div>
            </fieldset>
            
            <div className="mt4">
              <input
                onClick={this.onSubmitSignIn}
                className="b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib"
                type="submit"
                value="Register"
              />
            </div>
            <div className="lh-copy mt2">
              <p  onClick={() => onRouteChange('signin')} className="f6 link dim black db pointer">Already an user? Sign In</p>
            </div>
          </div>
        </main>
      </article>
    );
  }
}

export default Register;