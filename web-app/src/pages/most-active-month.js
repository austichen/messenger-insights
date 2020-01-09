import React from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import { SubHeader, NextButton, Graph } from '../components'
import SEO from '../components/seo'
import { PAGES } from '../utils/constants'
import { convertXYToObj } from '../utils/helpers'

const fullMonthName = {
    Jan: 'January',
    Feb: 'February',
    Mar: 'March',
    Apr: 'April',
    May: 'May',
    Jun: 'June',
    Jul: 'July',
    Aug: 'August',
    Sep: 'September',
    Oct: 'October',
    Nov: 'November',
    Dec: 'December',
}

const MostActiveMonth = ({ data }) => {
    const { x, y } = data.stats.edges[0].node.mostActiveMonth.data
    const mostActiveMonths = Object.entries(convertXYToObj(x, y))
        .sort((a, b) => a[1] - b[1])
        .map(v => v[0])
    const MAMLen = x.length

    return (
        <Layout pageNumber={3}>
            <SEO title="Most Active Month" />
            <SubHeader colour="grey">
                There are 12 months in a year, but you seemed to like{' '}
                <span className="pink">
                    {fullMonthName[mostActiveMonths[MAMLen - 1]]}
                </span>{' '}
                the most.
            </SubHeader>
            <Graph
                type="bar"
                x={x}
                y={y}
                xLabel="Month"
                yLabel="Number of Messages"
                title="Activity by Month"
            />
            <NextButton nextPage={PAGES[4]} />
        </Layout>
    )
}

export default MostActiveMonth

export const pageQuery = graphql`
    query {
        stats: allStatsJson {
            edges {
                node {
                    mostActiveMonth {
                        data {
                            x
                            y
                        }
                    }
                }
            }
        }
    }
`
