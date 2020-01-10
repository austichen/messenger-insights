import React from 'react'
import { Link } from 'gatsby'
import { graphql } from 'gatsby'

import { PageHeader, SubHeader } from '../components'
import Layout from '../components/layout'
import SEO from '../components/seo'

const IndexPage = ({data}) => (
    <Layout pageNumber={0}>
        <SEO title="Home" />
        <PageHeader colour="grey" style={{ paddingTop: '10%' }}>
            Hi, {data.stats.edges[0].node.metadata.name.split(' ')[0]}
        </PageHeader>
        <SubHeader>
            You've been using <span className="blue">Messenger</span> since{' '}
            <span className="teal">{data.stats.edges[0].node.metadata.startYear}</span>.
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

export const pageQuery = graphql`
    query {
        stats: allStatsJson {
            edges {
                node {
                    metadata {
                        startYear
                        name
                    }
                }
            }
        }
    }
`
