import React from 'react'

const Container = ({className, children}) => {
  return (
    <div className={"mx-auto bg-[#FFCB05] rounded-lg p-2 m-1 " + className}>
      {children}
    </div>
  )
}

export default Container
