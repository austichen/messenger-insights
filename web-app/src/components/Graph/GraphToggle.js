import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Graph from './Graph'
import Toggle from '../Toggle'

const GraphToggle = ({ ys, yToggleLabels, ...props }) => {
    const [activeDataset, setActiveDataset] = useState(ys[0])

    return (
        <div className="graph-container" style={{ position: 'relative' }}>
            <Toggle
                labels={yToggleLabels}
                onClick={(_, index) => setActiveDataset(ys[index])}
            />
            <Graph y={activeDataset} {...props} />
        </div>
    )
}

GraphToggle.propTypes = {
    type: PropTypes.oneOf(['bar', 'line']).isRequired,
    x: PropTypes.array.isRequired,
    ys: PropTypes.arrayOf(
        PropTypes.oneOfType([
            PropTypes.arrayOf(PropTypes.number),
            PropTypes.objectOf(PropTypes.arrayOf(PropTypes.number)),
        ])
    ).isRequired,
    yToggleLabels: PropTypes.arrayOf(PropTypes.string).isRequired,
    xLabel: PropTypes.string.isRequired,
    yLabel: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
}

export default GraphToggle
