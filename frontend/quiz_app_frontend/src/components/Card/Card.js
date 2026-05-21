import React from 'react';

const Card = (props) => {
  return (
    <div className='tc grow bg-light-yellow br3 pa3 ma2 dib bw2 shadow-5'>
      <img alt='robots' style={{height:'200px', width:'200px'}} className="pointer" onClick={() => props.onCourseSelect(props.idx)} src={`https://robohash.org/${props.course_code}?200x200`} />
      <div>
        <h2 className="f5 lh-copy measure mt2 black link pointer" onClick={() => props.onCourseSelect(props.idx)}>{props.course_code}: {props.course_name}</h2>
      </div>
    </div>
  );
}

export default Card;