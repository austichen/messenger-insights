import React, { useEffect } from "react"
import { graphql } from "gatsby"
import Chart from "chart.js"

import Layout from "../components/layout"
import { SubHeader, NextButton } from "../components"
import SEO from "../components/seo"
import { PAGES } from "../utils/constants"

const numToEnglishString = n => {
  if (n >= 1000000000000) {
    return String(Math.floor(n / 1000000000000)) + " trillion"
  } else if (n >= 1000000000) {
    return String(Math.floor(n / 1000000000)) + " billion"
  } else if (n >= 1000000) {
    return String(Math.floor(n / 1000000)) + " million"
  } else {
    return n.toLocaleString()
  }
}

const MessagesPerYear = ({ data }) => {
  const { x, y } = data.stats.edges[0].node.messagesPerYear.data
  const {
    mostActiveYears,
    totalMessages,
  } = data.stats.edges[0].node.messagesPerYear.observations
  // const unpartitionedMPY = {}
  // Object.entries(messagesPerYear).forEach(([key, value]) => {
  //   unpartitionedMPY[key] = value.dm + value.gc;
  // });

  const messagesPerYear = {}
  const unpartitionedMPY = {}
  x.forEach((year, idx) => {
    const strYear = String(year)
    const { gc, dm } = y[idx]
    messagesPerYear[strYear] = y[idx]
    unpartitionedMPY[strYear] = gc + dm
  })

  // const mostActiveYears = Object.entries(unpartitionedMPY).sort((a, b) => a[1] - b[1]);

  const totalMessagesStr = numToEnglishString(totalMessages)
  const numYears = x.length
  const MAYLen = mostActiveYears.length

  return (
    <Layout pageNumber={1}>
      <SEO title="Page two" />
      <SubHeader colour="grey">
        You've sent <span className="purple">{totalMessagesStr}</span> messages
        over <span className="violet">{numYears}</span> years...
      </SubHeader>
      <h2>
        {" "}
        Your most active years were{" "}
        <span className="green">{mostActiveYears[MAYLen - 1]}</span>,{" "}
        <span className="yellow">{mostActiveYears[MAYLen - 2]}</span>, and{" "}
        <span className="orange">{mostActiveYears[MAYLen - 3]}</span>
      </h2>
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
            observations {
              mostActiveYears
              totalMessages
            }
          }
        }
      }
    }
  }
`
