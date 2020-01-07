import React from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import { SubHeader, NextButton, Graph} from '../components'
import SEO from '../components/seo'
import { PAGES } from '../utils/constants'
import { groupPartitionedData } from '../utils/helpers'

const TopGcs = ({ data }) => {
    const { x, y } = data.stats.edges[0].node.topGcs.data
    const topGroupChatNames = x.map((chat, i) => [chat, y[i]])
        .sort((a, b) => a[1] - b[1])
        .map(v => v[0])
        .reverse()

    return (
        <Layout pageNumber={4}>
            <SEO title="Page two" />
            <SubHeader colour="grey">
                When it came to group chats,{' '}
                <span className="red">{topGroupChatNames[0]}</span> was always lit
            </SubHeader>
            <h2>
                But <span className="green">{topGroupChatNames[1]}</span>, and{' '}
                <span className="orange">{topGroupChatNames[2]}</span> were tough
                competition
            </h2>
            <Graph
                style={{marginTop: '30px'}}
                type="bar"
                x={x}
                y={y}
                xLabel="Group Chat"
                yLabel="Number of Messages"
                title="Top Group Chats"
            />
            <NextButton nextPage={PAGES[5]} />
        </Layout>
    )
}

export default TopGcs

export const pageQuery = graphql`
    query {
        stats: allStatsJson {
            edges {
                node {
                    topGcs {
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
