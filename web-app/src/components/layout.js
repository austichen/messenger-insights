/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from 'react'
import PropTypes from 'prop-types'

import PageNumber from './PageNumber'
import './layout.css'

const Layout = ({ pageNumber, children }) => {
    return (
        <>
            <div
                style={{
                    margin: `0 auto`,
                    width: '90%',
                    height: '100vh',
                }}
            >
                <main>
                    <PageNumber pageNumber={pageNumber} />
                    {children}
                </main>
                {/* <footer>
          © {new Date().getFullYear()}, Built with
          {` `}
          <a href="https://www.gatsbyjs.org">Gatsby</a>
        </footer> */}
            </div>
        </>
    )
}

Layout.propTypes = {
    children: PropTypes.node.isRequired,
}

export default Layout
