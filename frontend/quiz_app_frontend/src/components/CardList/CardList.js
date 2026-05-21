import React from 'react';
import Card from '../Card/Card';
import Add from '../Add/Add'

const CardList = (props) => {
  const allCards = props.courses.map((user, i) => {
          return (
            <React.Fragment>
            <Card
              key={props.courses[i].id}
              course_code={props.courses[i].course_code}
              course_name={props.courses[i].course_name}
              idx = {i}
              onCourseSelect = {props.onCourseSelect}
              />
              </React.Fragment>
          );
        });
  return (
    <div>
      {allCards}
      <Add text="Course" onRouteChange={props.onRouteChange} route="CreateCourse" />
    </div>
  );
}

export default CardList;