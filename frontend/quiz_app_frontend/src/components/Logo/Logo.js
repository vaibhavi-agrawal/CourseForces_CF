import React from 'react';
import Tilt from './Tilt';
import './Logo.css'
import cf from './cf.png'

const Logo = ({isSignedIn,onRouteChange}) => {
	return(
		<div className='ma4 mt4 w-25'>
			<Tilt className="Tilt br2 shadow-2" max={50} style={{ height: 120, width: 130 }} >
			 <div className="Tilt-inner pointer"> <img src={cf} onClick={isSignedIn? ()=> onRouteChange('home'): ()=>onRouteChange('signin')} alt = "logo" style={{paddingTop:'5px', height:'110px'}}/> </div>
			</Tilt>
		</div>

	);
}

export default Logo;