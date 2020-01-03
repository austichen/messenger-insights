import PropTypes from 'prop-types'
import React, { useState } from 'react'

const toggleItemStyle = {
    fontSize: '0.55rem',
    border: '1px solid black',
    'border-radius': '5px',
    display: 'inline-block',
    padding: '0 4px',
    margin: '0 2px',
    cursor: 'pointer',
    '&:hover': {
        color: '#1b1c1d',
    },
}

const Toggle = ({ labels, onClick, ...props }) => {
    const [activeIndex, setActiveIndex] = useState(0)
    return (
        <div className="toggle" style={props.style}>
            {labels.map((label, i) => (
                <span
                    style={toggleItemStyle}
                    key={i}
                    className={i === activeIndex ? 'green' : 'grey'}
                    onClick={() => {
                        setActiveIndex(i)
                        onClick(label, i)
                    }}
                >
                    {label}
                </span>
            ))}
        </div>
    )
}

Toggle.propTypes = {
    labels: PropTypes.array.isRequired,
    onClick: PropTypes.func,
}

Toggle.defaultProps = {
    onClick: () => {},
}

export default Toggle
