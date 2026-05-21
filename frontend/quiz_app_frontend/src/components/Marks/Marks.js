import React from 'react';

const Marks = (props) => {
  return (
  	<div>
	    <li className="flex items-center lh-copy pa3 ph0-l bb b--black-10">
		      <img alt="avatar" className="w2 h2 w3-ns mr5 h3-ns br-100" src={`https://robohash.org/${props.username}.png/size=200x200?set=set3`} />
		      <div className="pl3 flex-auto">
		        <span className="f4 db black">{props.name}</span>
		        <span className="f6 db black-70">@{props.username}</span>
		      </div>
		       <h3 className="ml6 f4 serif"> {props.marks} </h3>
		      
		</li>
     </div>
  );
}

export default Marks;