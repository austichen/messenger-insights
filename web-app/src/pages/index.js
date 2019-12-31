import React from "react"
import { Link } from "gatsby"
import { Header, Button } from "semantic-ui-react"

import PageHeader from "../components/pageHeader"
import SubHeader from "../components/subHeader"
import Layout from "../components/layout"
import Image from "../components/image"
import SEO from "../components/seo"

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <PageHeader style={{paddingTop: '10%'}}>Hi, Austin</PageHeader>
    <SubHeader>You've been using <span className="blue-text">Messenger</span> since <span className="teal-text">2010</span>.</SubHeader>
    <SubHeader>Why don't we take a stroll down memory lane?</SubHeader>
    <Link to="/messages-per-year/"><Header color="green" style={{fontSize: '5rem', marginTop: '10px'}}>Click here to begin</Header></Link>
  </Layout>
)

export default IndexPage
