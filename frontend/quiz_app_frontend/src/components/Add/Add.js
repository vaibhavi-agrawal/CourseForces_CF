import React from 'react';
import symbol from './add.png'

const Add = (props) => {
  return (
    <div className='tc grow bg-light-yellow pointer br3 pa3 ma2 dib bw2 shadow-5'>
      <img alt='add' onClick= {() => props.onRouteChange(props.route)} style={{height:'200px', width:'200px'}} src={symbol} />
      <div>
        <h2 className="f5 lh-copy measure mt2 black" onClick= {() => props.onRouteChange(props.route)}>Add a {props.text}</h2>
      </div>
    </div>
  );
}

export default Add;