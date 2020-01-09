import PropTypes from 'prop-types'
import React from 'react'
import { Link } from 'gatsby'

const style = {
    position: 'absolute',
    bottom: '50px',
    right: '50px',
}

const NextButton = ({ nextPage }) => (
    <Link style={style} to={nextPage}>
        <span className="blue">Next></span>
    </Link>
)

NextButton.propTypes = {
    nextPage: PropTypes.string.isRequired,
}

export default NextButton
