import React from 'react'
import { Link } from 'gatsby'

import { PageHeader, SubHeader } from '../components'
import Layout from '../components/layout'
import SEO from '../components/seo'

const IndexPage = () => (
    <Layout pageNumber={0}>
        <SEO title="Home" />
        <PageHeader colour="grey" style={{ paddingTop: '10%' }}>
            Hi, Austin
        </PageHeader>
        <SubHeader>
            You've been using <span className="blue">Messenger</span> since{' '}
            <span className="teal">2010</span>.
        </SubHeader>
        <SubHeader>Why don't we take a stroll down memory lane?</SubHeader>
        <SubHeader>
            <Link className="green" to="/messages-per-year/">
                Click here to begin
            </Link>
        </SubHeader>
    </Layout>
)

export default IndexPage
