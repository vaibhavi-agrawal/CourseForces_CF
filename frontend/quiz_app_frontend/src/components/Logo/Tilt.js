import React, { useRef } from 'react';

const Tilt = ({ children, className, style, max = 50 }) => {
	const ref = useRef(null);

	const handleMouseMove = (e) => {
		const el = ref.current;
		if (!el) return;
		const rect = el.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;
		const rotateX = ((y - rect.height / 2) / (rect.height / 2)) * (max / 2) * -1;
		const rotateY = ((x - rect.width / 2) / (rect.width / 2)) * (max / 2);
		el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
	};

	const handleMouseLeave = () => {
		if (ref.current) ref.current.style.transform = '';
	};

	return (
		<div
			ref={ref}
			className={className}
			style={style}
			onMouseMove={handleMouseMove}
			onMouseLeave={handleMouseLeave}
		>
			{children}
		</div>
	);
};

export default Tilt;
