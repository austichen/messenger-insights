import React from 'react'
import { graphql } from 'gatsby'
import Layout from '../components/layout'
import { SubHeader, NextButton, GraphToggle } from '../components'
import SEO from '../components/seo'
import { PAGES } from '../utils/constants'
import { groupPartitionedData, sortXValuesDescending } from '../utils/helpers'

const numToEnglishString = n => {
    if (n >= 1000000000000) {
        return String(Math.floor(n / 1000000000000)) + ' trillion'
    } else if (n >= 1000000000) {
        return String(Math.floor(n / 1000000000)) + ' billion'
    } else if (n >= 1000000) {
        return String(Math.floor(n / 1000000)) + ' million'
    } else {
        return n.toLocaleString()
    }
}

const MessagesPerYear = ({ data }) => {
    const { x, y } = data.stats.edges[0].node.messagesPerYear.data
    const messagesPerYear = groupPartitionedData(y)
    const mostActiveYears = sortXValuesDescending(x, messagesPerYear.total)
    const totalMessagesStr = numToEnglishString(
        messagesPerYear.total.reduce((acc, numMessages) => acc + numMessages)
    )
    const numYears = x.length

    return (
        <Layout pageNumber={1}>
            <SEO title="Messages Per Year" />
            <SubHeader colour="grey">
                You've had <span className="purple">{totalMessagesStr}</span>{' '}
                messages over <span className="violet">{numYears}</span>{' '}
                years...
            </SubHeader>
            <h2>
                {' '}
                Your most active years were{' '}
                <span className="green">{mostActiveYears[0]}</span>,{' '}
                <span className="yellow">{mostActiveYears[1]}</span>, and{' '}
                <span className="orange">{mostActiveYears[2]}</span>
            </h2>

            <GraphToggle
                style={{ marginTop: '30px' }}
                type="bar"
                x={x}
                ys={[
                    messagesPerYear.total,
                    {
                        dms: messagesPerYear.dm,
                        'group chats': messagesPerYear.gc,
                    },
                ]}
                yToggleLabels={['Total', 'Partitioned']}
                xLabel="Year"
                yLabel="Number of Messages"
                title="Messages per Year"
            />
            <NextButton nextPage={PAGES[2]} />
        </Layout>
    )
}

export default MessagesPerYear

export const pageQuery = graphql`
    query {
        stats: allStatsJson {
            edges {
                node {
                    messagesPerYear {
                        data {
                            x
                            y {
                                dm
                                gc
                            }
                        }
                    }
                }
            }
        }
    }
`
