import React from 'react'
import PropTypes from 'prop-types'
import { COLOURS } from '../../utils/constants'

const style = {
    fontSize: '4.67rem',
    padding: '0.25rem 0 0.25rem 0',
}

const PageHeader = ({ colour, children, ...props }) => (
    <h1 className={colour} style={{ ...style, ...props.style }}>
        {children}
    </h1>
)

PageHeader.propTypes = {
    colour: PropTypes.oneOf(COLOURS),
}

PageHeader.defaultProps = {
    colour: `black`,
}

export default PageHeader
