import React from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import { SubHeader, GraphToggle } from '../components'
import SEO from '../components/seo'
import { groupPartitionedData } from '../utils/helpers'

const TopDms = ({ data }) => {
    const { x, y } = data.stats.edges[0].node.topDms.data
    const topMessages = groupPartitionedData(y)
    const topDmNames = x.map((chat, i) => [chat, y[i]])
        .sort((a, b) => a[1] - b[1])
        .map(v => v[0])
        .reverse()
    
    return (
        <Layout pageNumber={5}>
            <SEO title="Page two" />
            <h2 style={{marginTop: '20px'}}>
                Throughout all these years, one person had your attention in particular...
            </h2>
            <SubHeader colour="grey">
                You spent the most time talking to{' '}
                <span className="purple">{topDmNames[0]}</span>, with{' '}
                <span className="yellow">{topDmNames[1]}</span> and{' '}
                <span className="blue">{topDmNames[2]}</span> right behind
            </SubHeader>
            <GraphToggle
                style={{marginTop: '30px'}}
                type="bar"
                x={x}
                ys={[
                    topMessages.total,
                    {
                        me: topMessages.me,
                        them: topMessages.them,
                    },
                ]}
                yToggleLabels={['Total', 'Partitioned']}
                xLabel="Chat"
                yLabel="Number of Messages"
                title="Top DMs"
            />
        </Layout>
    )
}

export default TopDms

export const pageQuery = graphql`
    query {
        stats: allStatsJson {
            edges {
                node {
                    topDms {
                        data {
                            x
                            y {
                                me
                                them
                            }
                        }
                    }
                }
            }
        }
    }
`
