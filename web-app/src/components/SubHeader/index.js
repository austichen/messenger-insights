import PropTypes from 'prop-types'
import React from 'react'
import { COLOURS } from '../../utils/constants'

const style = {
    fontSize: '2.3rem',
    padding: '0.2rem 0 0.2rem 0',
}

const SubHeader = ({ colour, children, ...props }) => (
    <h2 className={colour} style={{ ...style, ...props.style }}>
        {children}
    </h2>
)

SubHeader.propTypes = {
    colour: PropTypes.oneOf(COLOURS),
}

SubHeader.defaultProps = {
    colour: `black`,
}

export default SubHeader
