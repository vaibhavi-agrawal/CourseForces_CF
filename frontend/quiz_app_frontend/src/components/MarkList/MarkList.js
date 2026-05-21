import React from 'react';
import Marks from '../Marks/Marks';

const MarkList = (props) => {
  const allStudents = props.marks.map((user, i) => {
          return (
          <div>
              <div className="measure center">
              <React.Fragment className="dt w-100 bb b--black-05 pb2 mt2">
              <Marks
                key={props.marks[i].user_pk}
                marks = {props.marks[i].total_marks}
                name={props.marks[i].name}
                username={props.marks[i].username}
                />
                </React.Fragment>
                </div>
              </div>
          );
        });
  return (
    <div>
      <h1 className="f1 mid-gray helvetica"> Marks List </h1>
      {allStudents}
      <button class="f6 link pointer br1 mt4 mr4 ph3 pv2 mb2 shadow-4 dib white bg-gray" onClick={() => props.onRouteChange('QuizInfoPage')} >Back</button>
    </div>
  );
}

export default MarkList;