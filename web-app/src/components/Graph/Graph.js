import React, { useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import Chart from 'chart.js'

const backgroundColours = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
]
const borderColours = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
]

const getDatasetAndShowLegend = (y, randIndex) => {
    if (Array.isArray(y)) {
        const datasets = [
            {
                data: y,
                backgroundColor: backgroundColours[randIndex],
                borderColor: borderColours[randIndex],
                borderWidth: 1,
            },
        ]
        const showLegend = false
        return { datasets, showLegend }
    } else {
        const datasets = Object.entries(y).map(([key, value], idx) => {
            return {
                label: key,
                data: value,
                backgroundColor:
                    backgroundColours[
                        (randIndex + idx + 1) % backgroundColours.length
                    ],
                borderColor:
                    borderColours[(randIndex + idx + 1) % borderColours.length],
                borderWidth: 1,
            }
        })
        const showLegend = true
        return { datasets, showLegend }
    }
}

const Graph = ({ type, x, y, xLabel, yLabel, title, ...props }) => {
    useEffect(() => {
        const { datasets, showLegend } = getDatasetAndShowLegend(
            y,
            randIndex.current
        )
        const options = {
            type,
            data: {
                labels: x,
                datasets,
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: xLabel,
                                fontSize: 18,
                                fontFamily: 'Lato',
                            },
                        },
                    ],
                    yAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: yLabel,
                                fontSize: 18,
                                fontFamily: 'Lato',
                            },
                        },
                    ],
                },
                legend: {
                    display: showLegend,
                },
                title: {
                    display: true,
                    text: title,
                    fontSize: 24,
                },
            },
        }
        if (currentGraph.current) {
            Object.entries(options).forEach(
                ([key, value]) => (currentGraph.current[key] = value)
            )
            currentGraph.current.update()
        } else {
            const newGraph = new Chart(canvasRef.current, options)
            currentGraph.current = newGraph
        }
    }, [type, x, y, xLabel, yLabel, title])

    const randIndex = useRef(
        Math.floor(Math.random() * (backgroundColours.length - 1))
    )
    const currentGraph = useRef()
    const canvasRef = useRef()
    return (
        <canvas
            ref={canvasRef}
            style={{ width: '100%', height: '60vh' }}
        ></canvas>
    )
}

Graph.propTypes = {
    type: PropTypes.oneOf(['bar', 'line']).isRequired,
    x: PropTypes.array.isRequired,
    y: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.number),
        PropTypes.objectOf(PropTypes.arrayOf(PropTypes.number)),
    ]).isRequired,
    xLabel: PropTypes.string.isRequired,
    yLabel: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
}

export default Graph
