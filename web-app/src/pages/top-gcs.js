import React from "react"
import { graphql } from "gatsby"

import Layout from "../components/layout"
import { SubHeader, NextButton } from "../components"
import SEO from "../components/seo"
import { PAGES } from "../utils/constants"

const TopGcs = ({ data }) => {
  const { x, y } = data.stats.edges[0].node.topGcs.data
  const topGcs = {}
  const unpartitionedTopGcs = {}
  x.forEach((name, idx) => {
    const { me, them } = y[idx]
    topGcs[name] = y[idx]
    unpartitionedTopGcs[name] = me + them
  })

  const topMessages = Object.entries(unpartitionedTopGcs)
    .sort((a, b) => a[1] - b[1])
    .map(v => v[0])
    .reverse()

  return (
    <Layout pageNumber={4}>
      <SEO title="Page two" />
      <SubHeader colour="grey">
        When it came to group chats,{" "}
        <span className="red">{topMessages[0]}</span> was always lit
      </SubHeader>
      <h2>
        But <span className="green">{topMessages[1]}</span>, and{" "}
        <span className="orange">{topMessages[2]}</span> were tough competition
      </h2>
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
