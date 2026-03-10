module.exports = { layout: (data) => data.layout === null ? null : (data.layout || 'base.njk') };
