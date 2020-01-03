import React from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import { SubHeader } from '../components'
import SEO from '../components/seo'

const TopDms = ({ data }) => {
    const { x, y } = data.stats.edges[0].node.topDms.data
    const topDms = {}
    const unpartitionedTopDms = {}
    x.forEach((name, idx) => {
        const { me, them } = y[idx]
        topDms[name] = y[idx]
        unpartitionedTopDms[name] = me + them
    })

    const topMessages = Object.entries(unpartitionedTopDms)
        .sort((a, b) => a[1] - b[1])
        .map(v => v[0])
        .reverse()

    return (
        <Layout pageNumber={5}>
            <SEO title="Page two" />
            <SubHeader colour="grey">
                One person had your attention in particular...
            </SubHeader>
            <h2>
                You spent the most time talking to{' '}
                <span className="purple">{topMessages[0]}</span>, with{' '}
                <span className="yellow">{topMessages[1]}</span> and{' '}
                <span className="blue">{topMessages[2]}</span> right behind
            </h2>
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
