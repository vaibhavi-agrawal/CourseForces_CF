import React from 'react';
import './InviteForm.css';

const InviteForm = (props) => {
  return (
    <div className="ma5">
      <p className='f2 gray bold helvetica'>
        {`To invite users to ${props.course_code}, enter their email/username below`}
      </p>
      <div className='center'>
        <div className='form center pa4 br3 shadow-5'>
          <input className='f4 pa2 w-70 center' type='tex' onChange={props.onInputChange}/>
          <button
            className='w-30 grow f4 link ph3 pv2 dib pointer white bg-light-purple'
            onClick = {() => props.sendInvite()} >
          Send Invite! </button>
        </div>
      </div>
    </div>
  );
}

export default InviteForm;