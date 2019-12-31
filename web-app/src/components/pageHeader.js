import { Header } from "semantic-ui-react"
import PropTypes from "prop-types"
import React from "react"

const PageHeader = ({ children, ...props }) => (
  <Header color="grey" as="h1" style={{'font-size': '10rem', ...props.style}}>{children}</Header>

)

// Header.propTypes = {
//   siteTitle: PropTypes.string,
// }

// Header.defaultProps = {
//   siteTitle: ``,
// }

export default PageHeader
