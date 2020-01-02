import React from "react"
import { graphql } from "gatsby"

import Layout from "../components/layout"
import { SubHeader, NextButton } from "../components"
import SEO from "../components/seo"
import { PAGES } from "../utils/constants"
import { convertXYToObj } from "../utils/helpers";

const getMessageForHour = hour => {
  const morningHours = new Set([
    "5am",
    "6am",
    "7am",
    "8am",
    "9am",
    "10am",
    "11am",
  ])
  const afternoonHours = new Set([
    "12pm",
    "1pm",
    "2pm",
    "3pm",
    "4pm",
    "5pm",
    "6pm",
  ])
  const eveningHours = new Set(["7pm", "8pm", "9pm"])
  const nightHours = new Set(["10pm", "11pm", "12am"])
  const nocturnalHours = new Set(["1am", "2am"])
  const austinHours = new Set(["3am", "4am"])

  if (morningHours.has(hour)) {
    return "Looks like you're a real early bird."
  } else if (afternoonHours.has(hour)) {
    return "Nothing better than chill afternoons."
  } else if (eveningHours.has(hour)) {
    return "You had a lot of time to chat in the evenings."
  } else if (nightHours.has(hour)) {
    return "Looks like you prefer to use Messenger from the comfort of your bed"
  } else if (nocturnalHours.has(hour)) {
    return "Gotta get those late night deep talks."
  } else if (austinHours.has(hour)) {
    return "Up early or awake late?"
  } else {
    return "owo uwu"
  }
}

const MessagesPerYear = ({ data }) => {
  const { x, y } = data.stats.edges[0].node.mostActiveHour.data
  const mostActiveHours = Object.entries(convertXYToObj(x, y))
    .sort((a, b) => a[1] - b[1])
    .map(v => v[0])
  const MAHLen = x.length
  const activityMessage = getMessageForHour(mostActiveHours[MAHLen - 1])

  return (
    <Layout pageNumber={2}>
      <SEO title="Page two" />
      <SubHeader colour="grey">
        You were most active at{" "}
        <span className="teal">{mostActiveHours[MAHLen - 1]}</span>
      </SubHeader>
      <h2>{activityMessage}</h2>
      <NextButton nextPage={PAGES[3]} />
    </Layout>
  )
}

export default MessagesPerYear

export const pageQuery = graphql`
  query {
    stats: allStatsJson {
      edges {
        node {
          mostActiveHour {
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
