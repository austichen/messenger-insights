import React from "react"
import PropTypes from "prop-types"
import { Link } from "gatsby"
import { PAGES } from "../../utils/constants"

const style = {
  position: "absolute",
  top: "20px",
  right: "50px",
}

const PageNumber = ({ pageNumber, children, ...props }) => (
  <div className="page-number grey" style={style}>
    {pageNumber !== 0 && (
      <Link className="blue" to={PAGES[pageNumber - 1]}>
        {"<"}
      </Link>
    )}
    {`${pageNumber + 1}/${PAGES.length}`}
    {pageNumber !== PAGES.length - 1 && (
      <Link className="blue" to={PAGES[pageNumber + 1]}>
        {">"}
      </Link>
    )}
  </div>
)

PageNumber.propTypes = {
  pageNumber: PropTypes.number.isRequired,
}

export default PageNumber
